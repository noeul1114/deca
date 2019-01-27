"""
Django settings for tutorialPoll project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from datetime import datetime
import uuid
import posixpath

from django.conf.global_settings import TEMPLATES
from .custom_upload_path import custom_uploaded_filepath_debug, custom_uploaded_filepath_deploy \
 ,custom_uploaded_filepath_debug_board_image, custom_uploaded_filepath_deploy_board_image \
, custom_uploaded_filepath_debug_thumb_image, custom_uploaded_filepath_deploy_thumb_image


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+c1@o4ikm@!1s+!wcqdtuaab*c_&3pphnkh7wgmek9v^)uqg8-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    custom_uploaded_filepath = custom_uploaded_filepath_debug
else:
    custom_uploaded_filepath = custom_uploaded_filepath_deploy

if DEBUG:
    BOARD_IMAGE_UPLOADPATH = custom_uploaded_filepath_deploy_board_image
else:
    BOARD_IMAGE_UPLOADPATH = custom_uploaded_filepath_deploy_board_image

if DEBUG:
    THUMB_IMAGE_UPLOADPATH = custom_uploaded_filepath_deploy_thumb_image
else:
    THUMB_IMAGE_UPLOADPATH = custom_uploaded_filepath_deploy_thumb_image

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls',
    'boards',
    'todaycomment',
    'django_summernote',
    'storages',
    'rest_framework',
    'router',
    'el_pagination',
    'phonenumber_field',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tutorialPoll.middleware.AttachmentMiddleware'
]

ROOT_URLCONF = 'tutorialPoll.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request', ## For EL-pagination
            ],
        },
    },
]

WSGI_APPLICATION = 'tutorialPoll.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'sayproject',
            'USER': 'django',
            'PASSWORD': 'qudtlstz1',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }




# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

if DEBUG:
    SUMMERNOTE_CONFIG = {

        'summernote': {
            # As an example, using Summernote Air-mode
            'airMode': False,

            # Change editor size
            'width': '100%',
            'height': '900',

            # Use proper language setting automatically (default)
            'lang': None,

            # Or, set editor language/locale forcely
            'lang': 'ko-KR',

            # You can add custom css/js for SummernoteWidget.
            'css': (
            ),
            # 'js': ('$(".summernote").summernote({onMediaDelete : function($target, editor, $editable) {console.log($target.context.dataset.filename);$target.remove();console.log("all gone!");}})'
            #
            # ),
        },

        'attachment_upload_to': custom_uploaded_filepath,

        'attachment_model': 'boards.Attachment'
    }
else:
    SUMMERNOTE_CONFIG = {

        'summernote': {
            # As an example, using Summernote Air-mode
            'airMode': False,

            # Change editor size
            'width': '100%',
            'height': '900',

            # Use proper language setting automatically (default)
            'lang': None,

            # Or, set editor language/locale forcely
            'lang': 'ko-KR',

            # You can add custom css/js for SummernoteWidget.
            'css': (
            ),
            # 'js': ('$(".summernote").summernote({onMediaDelete : function($target, editor, $editable) {console.log($target.context.dataset.filename);$target.remove();console.log("all gone!");}})'
            #
            # ),
        },

        'attachment_upload_to': custom_uploaded_filepath,

        'attachment_storage_class': 'storages.backends.ftp.FTPStorage',

        'attachment_model': 'boards.Attachment'
    }

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 30
}


if DEBUG:
    MEDIA_URL = '/'
    BOARD_IMG_FTP = 'http://thl1110.jpg2.kr/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
else:
    MEDIA_URL = 'http://thl1110.jpg2.kr/'
    BOARD_IMG_FTP = 'http://thl1110.jpg2.kr/'
    MEDIA_ROOT = '/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

if DEBUG:
    # For development
    STATIC_URL = '/staticfiles/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    FTP_STORAGE_LOCATION = 'ftp://thl1110:qudtlstz1@thl1110.jpg2.kr:21'
else:
    # For deployment
    STATIC_URL = 'https://willypower.cafe24.com/staticfiles/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    FTP_STORAGE_LOCATION = 'ftp://thl1110:qudtlstz1@thl1110.jpg2.kr:21'

# For deployment
# STATIC_URL = 'http://thl1110.jpg2.kr/staticfiles/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


