"""
Django settings for datajoiner project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_PATH = BASE_DIR


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8(4j+v!$pv91yr_9@n4)9$3zd2ntfnh*+n&=1h^(5fb+^id48k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'kombu.transport.django',
    #'debug_toolbar',
    'emailuser',
    'bootstrapform',
    'itsdangerous',
    'tastypie',
    
    'inmagik_utils',
    'userdata',
    'ui',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'datajoiner.urls'

WSGI_APPLICATION = 'datajoiner.wsgi.application'

import django.conf.global_settings as DEFAULT_SETTINGS
TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + ('django.core.context_processors.request',)



# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('en-us', _('English')),
    #('it', _('Italian')),
)

LOCALE_PATHS = (
    os.path.join(BASE_PATH, "locale"),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_PATH, "assets"),
)

STATIC_ROOT = os.path.join(BASE_PATH, "static_collected")

MEDIA_ROOT =  os.path.join(BASE_PATH, "media")

MEDIA_URL = '/media/'


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_PATH, "templates"),
)


from django.core.urlresolvers import reverse_lazy
AUTH_USER_MODEL = "emailuser.EmailUser"

#login
LOGIN_URL = reverse_lazy("login")
LOGOUT_URL = reverse_lazy("logout")
LOGIN_REDIRECT_URL = reverse_lazy("home")
LOGIN_AFTER_REGISTER = True
REGISTER_REDIRECT_URL = LOGIN_REDIRECT_URL


#email settings
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_PATH, "tmp")
DEFAULT_FROM_EMAIL = "info@inmagik.com"


#signing settings
SIGNING_KEY = "uHuH1TH1SiS0M3TH1NG1v3ryD1ff56icuLtT0G74ues7sSANDDuW1LLn=T"
MAX_TOKEN_AGE = 172800


#celery stuff
BROKER_URL = 'django://'

CELERY_RESULT_BACKEND = 'djcelery.backends.database.DatabaseBackend'

