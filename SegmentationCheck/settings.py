"""
Django settings for SegmentationCheck project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import djcelery

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^49jkh@wk!6by03j4f@du(m3$)1-%yejr!@om&#tm974b3%99i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition


DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
#   'qiniustorage',
    'django_extensions',
    'rest_framework',
    'djcelery',
#    'kombu.transport.django',
]

LOCAL_APPS = [
    'home',
    'account',
    'catalogue',
    'managerawdata',
    'preprocess',
    'segmentation',
    'layoutseg',
    'charseg',
    'characters',
    'pagecheck',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

djcelery.setup_loader()
#BROKER_URL = 'django://'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'SegmentationCheck.urls'

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
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SegmentationCheck.wsgi.application'

REST_FRAMEWORK = {
    'UNICODE_JSON': False,
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "api.pagination.StandardPagination",
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.DjangoFilterBackend",
    ),
}

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dzj_characters',
        'USER': 'dzj',
        'PASSWORD': 'dzjsql',
        #'HOST': '192.168.16.100',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTH_PROFILE_MODULE = 'account.UserProfile'

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/' # It means home view
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'
MEDIA_ROOT = '/data/share/dzj_characters/'
MEDIA_URL = '/'

#DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuStorage'
#STATICFILES_STORAGE = 'qiniustorage.backends.QiniuStaticStorage'
COVER_IMAGE_ROOT = MEDIA_ROOT+'cover/'
OPAGE_IMAGE_ROOT = MEDIA_ROOT+'opage_images/'
PAGE_IMAGE_ROOT = MEDIA_ROOT+'page_images/'
CHARACTER_IMAGE_ROOT = MEDIA_ROOT+'character_images/'

STATIC_ROOT = "/site_media/static"
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, 'frontend', 'build'),
)

QINIU_ACCESS_KEY= ''
QINIU_SECRET_KEY= ''
QINIU_BUCKET_DOMAIN= ''
QINIU_BUCKET_NAME= ''

QINIU_SECURE_URL = False

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/segmentation_web.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


