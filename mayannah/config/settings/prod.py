from .base import *
import environ

root = environ.Path(__file__) -3
env = environ.Env()
environ.Env.read_env(root.path('prod.env')())

DEBUG = False


INSTALLED_APPS += [
    'partner',
    'rest_framework',
    'virtual_money',
    'raven.contrib.django.raven_compat',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'person',
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

AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
        )
SITE_ID = 1
LOGIN_REDIRECT_URL = 'profile:self'
ACCOUNT_EMAIL_VERIFICATION = 'none'

# DJANGO REST FRAMEWORK settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
                ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.BasicAuthentication',
    ),
}

# JWT SETTINGS
JWT_AUTH = {
        'JWT_VERIFY_EXPIRATION': False,
}
