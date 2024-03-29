"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y+id0($s%7-c$49a3g1gzj15xcxu$emwjo*1yphr!2*q+iqq3@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'django_filters',
    'users',
    'core'
]

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'globals.middleware.LoggingMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'elector_recognizer',
        'USER': 'user_log',
        'PASSWORD': 'user_log',
        'HOST': '127.0.0.1',
        'PORT': ''
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT_ = os.path.join(BASE_DIR, "pictures")
MEDIA_ROOT = os.path.join(MEDIA_ROOT_, "electors")

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'globals.pagination.CustomPagination',
    'PAGE_SIZE': None,
    'EXCEPTION_HANDLER': 'globals.utils.core_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'errors',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=5),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(hours=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(hours=5),
}

CORS_ORIGIN_ALLOW_ALL = True

LOG_DIR = os.path.join(BASE_DIR, "log")

UPLOAD_DIR = os.path.join(BASE_DIR, "pictures") + os.sep + "unknowns"
UPLOAD_DIR_ELECTOR = os.path.join(BASE_DIR, "pictures") + os.sep + "electors"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'large': {
            'format': '%(asctime)s  %(levelname)s  %(process)d  %(pathname)s  %(funcName)s  %(lineno)d  %(message)s  '
        },
        'tiny': {
            'format': '%(asctime)s  %(message)s  '
        }
    },
    'handlers': {
        'access_file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, "access.log"),
            'formatter': 'large',
        },
        'http_client_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, "http_client.log"),
            'formatter': 'large',
        },
        'errors_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, "errors.log"),
            'formatter': 'large',
        }
    },
    'loggers': {
        'access_file': {
            'handlers': ['access_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'http_client_file': {
            'handlers': ['http_client_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'errors_file': {
            'handlers': ['errors_file'],
            'level': 'ERROR',
            'propagate': False,
        }
    },
}

SMS_API = {
    'BULK': {
        'BASE_URL': 'https://portail.lmtgroup.com',
        'URI': '/api/providers/bulksms/send-sms',
        'METHOD': 'POST',
        'API_KEY': 'EB2E629AE43C9926B7D6D511FB643F5E',
        'PASSWORD': 'B91D8A24-A47C-33B5-9E2D-02DAE1056A15'
    }
}

# Excel Template folder and files
TEMPLATE_ROOT = os.path.join(BASE_DIR, "private")

TEMPLATE_ROOT_VOTE_FILE = os.path.join(TEMPLATE_ROOT, 'template_votes.xlsx')
