"""
Django settings for jobboard_backend project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3=7dn5z9mn8^q-%y4dip5w*r^y6_v9n0(ksoa+mge_ngrc#16p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'realtimejobs',
    'rest_framework_simplejwt',
    'django_celery_beat',
    'django_ckeditor_5',

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

ROOT_URLCONF = 'jobboard_backend.urls'

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

WSGI_APPLICATION = 'jobboard_backend.wsgi.application'

AUTH_USER_MODEL = 'realtimejobs.User'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 'default': dj_database_url.config(default=os.getenv('DATABASE_URL'), engine='django.db.backends.mysql'),
        'NAME': os.getenv('DB_NAME'),
        'USER':  os.getenv('DB_USER'),
        'PASSWORD':  os.getenv('DB_PASSWORD'),
        'HOST':  os.getenv('DB_HOST'),
        # Default MySQL port is 3306
        'PORT':  os.getenv('DB_PORT', default='3306'),
    }
}


# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"


# chapa API secret key and Publick key
CHAPA_SECRET_KEY = os.getenv('CHAPA_SECRET_KEY')
CHAPA_PUBLIC_KEY = os.getenv('CHAPA_PUBLIC_KEY')

CHAPA_CALLBACK_URL = 'http://127.0.0.1:8000/verify_payment/'

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=600),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,  # Generates a new refresh token on refresh
    "BLACKLIST_AFTER_ROTATION": True,  # Invalidates old refresh tokens
    "ALGORITHM": "HS256",
}

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Configure Django to send emails using Gmail

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Use your email provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|', 'bold', 'italic', 'link',
            'bulletedList', 'numberedList', 'blockQuote',
           '|', 'alignment:left', 'alignment:center',
            'alignment:right', 'alignment:justify', '|',  # Alignment options
            'fontColor',  # Text color options
        ],
        'language': 'en',
        'alignment': {
            'options': ['left', 'center', 'right', 'justify']
        },
        'fontColor': {
            'colors': [
                {
                    'color': 'black',
                    'label': 'Black',
                    'default': True,
                },
               
            ],
            'columns': 1  # Arranges colors in 4 columns
        },
    },
}

CKEDITOR_5_CUSTOM_CSS = '/ckstatic/custom_styles.css'
