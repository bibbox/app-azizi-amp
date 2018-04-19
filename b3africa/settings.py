"""
Django settings for marsabit project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import json

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
if 'MYSQL_DATABASE' in os.environ:
    STATICFILES_DIRS = (
        os.path.join(SITE_ROOT, '/opt/azizi_amp/static/'),
    )
else:
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static'))
    STATICFILES_DIRS = (
        os.path.join(SITE_ROOT, static_path),
    )

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xw9xyc$nyym$q0-3-pozdek-f0o_z1xpktpm8ex36k9g&0464v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'livereload',
    'raven.contrib.django.raven_compat',

    'easy_thumbnails',
    'b3africa',
    'odk_dashboard',
    'vendor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'livereload.middleware.LiveReloadScript',
]

ROOT_URLCONF = 'b3africa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'templates/jinja2'), os.path.join(BASE_DIR, 'odk_dashboard/templates/jinja2')],
        'APP_DIRS': True,
        'OPTIONS': {'environment': 'b3africa.jinja2_settings.environment',},
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/django')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'b3africa.wsgi.application'

SITE_NAME = 'Azizi - AMP'

DEFAULT_REPORTING_PERIOD = 30

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# either use the environment variables or variables defined in a config file
if 'MYSQL_DATABASE' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['MYSQL_DATABASE'],
            'DRIVER': 'mysql',
            'USER': os.environ['MYSQL_USER'],
            'PASSWORD': os.environ['MYSQL_PASSWORD'],
            'HOST': os.environ['MYSQL_HOST'],
            'PORT': os.environ['MYSQL_PORT']
        }
    }
else:
    with open('b3africa/app_config.json') as config_file:
        configs = json.load(config_file)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': configs['default']['db'],
                'USER': configs['default']['user'],
                'DRIVER': 'mysql',
                'PASSWORD': configs['default']['passwd'],
                'HOST': configs['default']['host'],
                'PORT': configs['default']['port'],
                'OPTIONS': {
                    'sql_mode': 'TRADITIONAL',
                    'charset': 'utf8',
                    'init_command': 'SET storage_engine=INNODB, character_set_connection=utf8, collation_connection=utf8_bin'
                }
            }
        }
        if DATABASES['default']['DRIVER'] == 'mysql':
            DATABASES['default']['OPTIONS'] = {
                'sql_mode': 'TRADITIONAL',
                'charset': 'utf8',
                'init_command': 'SET storage_engine=INNODB, character_set_connection=utf8, collation_connection=utf8_bin'
                # 'init_command': 'SET storage_engine=INNODB, character_set_connection=utf8, collation_connection=utf8_bin, SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',
            }  # Now we have a mild degree of confidence :-)


CRONJOBS = [
    # ('*/5 * * * *', 'marsabit.odk_forms.auto_process_submissions', '>> /tmp/marsabit_cron.log')
]


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = 'static/'

DEFAULT_LOCALE = 'English'

LOCALES = {
    'English': 'en'
}

LOOKUP_TABLE = 'dictionary_items'

# The number of records to use for the dry run
IS_DRY_RUN = False
DRY_RUN_RECORDS = 30

TEMPDIR = 'temp'

ERR_CODES = {
    'duplicate': {'CODE': 10001, 'TAG': 'DUPLICATE'},
    'data_error': {'CODE': 10002, 'TAG': 'INVALID DATA'},
    'fk_error': {'CODE': 10003, 'TAG': 'MISSING FK'},
    'unknown': {'CODE': 10004, 'TAG': 'UNKNOWN ERROR'}
}

JOINER = ' - '

GPS_REGEX = '-?\d{1,3}\.\d+\s-?\d{1,3}\.\d+\s\d{1,5}\.\d+\s\d{1,4}\.\d{1,2}'

# ##################  MEDIA ##################
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
PROFILE_PHOTO_DIR = ('uploads/profiles')  # If you change this
#                           Remember to update the model Profile

# ################# EMAIL SETTINGS ###########
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'me@gmail.com'
EMAIL_HOST_PASSWORD = 'password'

ABSOLUTE_ROOT = 'http://localhost:8011/'
SENTRY_LOCALHOST = 'http://a0dadd9f4bd54347b14d969b3f7fbdc1:e937cf83cee44449bf4bc5dfc64e70e6@localhost:9000/3'
SENTRY_PRODUCTION = 'http://412f07efec7d461cbcdaf686c3b01e51:c684fccd436e46169c71f8c841ed3b00@sentry.badili.co.ke/3'
