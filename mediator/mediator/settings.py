"""
Django settings for mediator project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os


def truthy(string):
    return string.lower() not in ('0', 'false', 'no')


# OpenHIM mediator settings

OPENHIM_OPTIONS = {
    'username': os.environ['OPENHIM_USERNAME'],
    'password': os.environ['OPENHIM_PASSWORD'],
    'apiURL': os.environ['OPENHIM_APIURL'],
    'verify_cert': truthy(os.environ['OPENHIM_VERIFY_CERT']),

    'force_config': False,
    'interval': 10,

    'register': truthy(os.environ['OPENHIM_REGISTER']),
    'heartbeat': truthy(os.environ['OPENHIM_HEARTBEAT']),
}

MEDIATOR_CONF = {
    'urn': f'urn:uuid:{os.environ["MEDIATOR_URN"]}',
    'version': '0.0.1',
    'name': os.environ['MEDIATOR_NAME'],
    'description': os.environ['MEDIATOR_DESCRIPTION'],
    'defaultChannelConfig': [
        {
            'name': os.environ['MEDIATOR_NAME'],
            'urlPattern': os.environ['MEDIATOR_URL'],
            'alerts': [],
            'txRerunAcl': [],
            'txViewFullAcl': [],
            'txViewAcl': [],
            'properties': [],
            'matchContentTypes': [],
            'routes': [
                {
                    'name': os.environ['MEDIATOR_ROUTE_0_NAME'],
                    'host': os.environ['MEDIATOR_ROUTE_0_HOST'],
                    'port': os.environ['MEDIATOR_ROUTE_0_PORT'],
                    'primary': True,
                    'type': 'http',
                }
            ],
            'allow': [os.environ['MEDIATOR_ALLOW_ROLE']],
            'type': 'http',
        }
    ],
    'endpoints': [
        {
            'name': os.environ['MEDIATOR_ROUTE_0_NAME'],
            'host': os.environ['MEDIATOR_ROUTE_0_HOST'],
            'path': os.environ['MEDIATOR_ROUTE_0_PATH'],
            'port': os.environ['MEDIATOR_ROUTE_0_PORT'],
            'primary': True,
            'type': 'http',
        }
    ]
}


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['DJANGO_DEBUG']

ALLOWED_HOSTS = os.environ['DJANGO_ALLOWED_HOSTS'].split()


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'tenants',
]

DATABASES = {
    'default': {
        'ENGINE': f'django.db.backends.{os.environ["DJANGO_DB_ENGINE"]}',
        'NAME': os.environ['DJANGO_DB_NAME'],
        'USER': os.environ['DJANGO_DB_USER'],
        'PASSWORD': os.environ['DJANGO_DB_PASSWORD'],
        'HOST': os.environ['DJANGO_DB_HOST'],
        'PORT': os.environ['DJANGO_DB_PORT'],
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mediator.urls'

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

WSGI_APPLICATION = 'mediator.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'mediator', 'static')
STATIC_URL = '/static/'

AUTH_USER_MODEL = 'tenants.TenantUser'
