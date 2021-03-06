"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$nt5%lgb0t!@kcs&(wa!1##7&t_&-$_czg!z%-xdygbb8jl=82'

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
    'api',
    'text',
    'user_profile',
    'kernel'
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

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
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

WSGI_APPLICATION = 'web.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    # '/var/www/static/',
]

from kombu import Queue
from kombu import Exchange

CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ['json', 'pickle']

# celery queues setup
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_ROUTING_KEY = 'default'

CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('MC_lm', exchange=Exchange('priority', type='direct'), routing_key='MC_lm'),
    Queue('MC_dep', exchange=Exchange('priority', type='direct'), routing_key='MC_dep'),
    Queue('MC_util', exchange=Exchange('priority', type='direct'), routing_key='MC_util'),

)

CELERY_BROKER_URL = 'amqp://misscut:misscut@166.111.226.247:5672/mc_vhost'  # Broker配置

CELERY_RESULT_BACKEND = "amqp://misscut:misscut@166.111.226.247:5672/mc_vhost"  # BACKEND配置

CELERY_ROUTES = ([
                     ('check_text_lm', {'queue': 'MC_lm', 'routing_key': 'MC_lm'}),
                     ('check_text_lm_for_swn', {'queue': 'MC_lm', 'routing_key': 'MC_lm'}),
                     ('check_text_dep_1', {'queue': 'MC_dep', 'routing_key': 'MC_dep'}),
                     ('check_text_dep_2', {'queue': 'MC_dep', 'routing_key': 'MC_dep'}),
                     ('check_text_dep_full', {'queue': 'MC_dep', 'routing_key': 'MC_dep'}),
                     ('preprocess', {'queue': 'MC_util', 'routing_key': 'MC_util'}),
                     ('collect_result_lm', {'queue': 'MC_util', 'routing_key': 'MC_util'}),
                     ('collect_result_dep', {'queue': 'MC_util', 'routing_key': 'MC_util'}),
                 ],)

# email

EMAIL_HOST = 'mails.tsinghua.edu.cn'  # 邮件服务器地址
EMAIL_PORT = 465  # 端口号25 or 465
EMAIL_HOST_USER = 'pxy18@mails.tsinghua.edu.cn'  # 用户名
EMAIL_HOST_PASSWORD = '05101314pW'  # 邮箱密码或授权码
EMAIL_USE_SSL = True
EMAIL_FROM = 'pxy18@mails.tsinghua.edu.cn'  # 发送人
