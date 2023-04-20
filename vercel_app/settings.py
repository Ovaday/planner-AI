"""
Django settings for vercel_app project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


from helpers.tokenHelpers import get_token, retrieve_and_cache_secrets, get_db_conn

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SECRETS = retrieve_and_cache_secrets()
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_token("DJANGO_SECRET")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_token("DEBUG_MODE")

ALLOWED_HOSTS = ['.vercel.app', '127.0.0.1', '3.72.87.62', get_token("AWS_HOST"), '*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
    'tg_bot',
    'django_q',
    'service_routine'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vercel_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'vercel_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# Note: Django modules for using databases are not support in serverless
# environments like Vercel. You can use a database over HTTP, hosted elsewhere.

DATABASES = {
    'default': get_db_conn()
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

import os.path
import sys


sentry_sdk.init(
    dsn=get_token("SENTRY_ENDPOINT"),
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
if get_token("VERCEL"):
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
    MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'

else:
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
    MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        os.path.join(PROJECT_ROOT, 'static'),
    )

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

Q_CLUSTER = {
    'name': get_token("Q_CLUSTER_NAME"),
    'workers': int(get_token("Q_CLUSTER_WORKERS")),
    'timeout': 60,
    'retry': 90,
    'queue_limit': 100,
    'attempt_count': 1,
    'ack_failures': True,
    'bulk': 5,
    'sqs': {
        'aws_region': get_token("IAM_AWS_REGION"),  # optional
        'aws_access_key_id': get_token("IAM_ACCESS_KEY"),  # optional
        'aws_secret_access_key': get_token("IAM_SECRET_KEY"),  # optional
        'receive_message_wait_time_seconds': 20
    }
}