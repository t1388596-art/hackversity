"""
Django settings for genai_project - DEVELOPMENT ENVIRONMENT

This configuration is specifically optimized for local development.
Simple, fast, and development-friendly settings.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Development Settings
SECRET_KEY = 'django-insecure-dev-key-for-hackversity-development-only-123456789'

# Always enable debug mode for development
DEBUG = False

# Development allowed hosts
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'testserver',
    '13.235.18.77'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'whitenoise.runserver_nostatic',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required for allauth
    
    # Third party apps
    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    # Local apps
    'accounts',
    'chat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'genai_project.urls'

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

WSGI_APPLICATION = 'genai_project.wsgi.application'


# Database - Simple SQLite for development

DATABASES={
    'default':{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':'backendcourse',
        'USER': 'mysuperuser',
        'PASSWORD': 'Mysuperuser',
        'HOST':'backendcourse.chms44cg0zaf.ap-south-1.rds.amazonaws.com',
        'PORT':'5432'
    }
}


# Password validation - Disabled for development (allows simple passwords)
AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files - Simple development configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Simple development cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Session Configuration - Simple for development
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  # HTTP OK for development

# Development logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Euron API Configuration
EURON_API_KEY = os.getenv('EURON_API_KEY', 'euri-94dee66c5f9b41981308651c7985cbf1db0ed7307f498e8e70ccc1da7c84c343')

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Django Authentication Configuration
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Authentication settings
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/chat/'
LOGOUT_REDIRECT_URL = '/'

# Allauth settings - Updated for django-allauth 0.63.6+
ACCOUNT_LOGIN_METHODS = ['username']  # Replaces ACCOUNT_AUTHENTICATION_METHOD
ACCOUNT_SIGNUP_FIELDS = ['username', 'password1', 'password2']  # Replaces ACCOUNT_EMAIL_REQUIRED and ACCOUNT_USERNAME_REQUIRED
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Email backend for development (prints to console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

print("🚀 Django GenAI Application - DEVELOPMENT MODE")
print("📝 Using SQLite database for development")
print("🔧 Debug mode enabled")
print("📧 Email backend: Console (emails will print to terminal)")

AWS_ACCESS_KEY_ID = 'AKIAT4ID72GEZ2HE2JPF'

AWS_SECRET_ACCESS_KEY = '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'

AWS_STORAGE_BUCKET_NAME = 'hackversity'

AWS_S3_SIGNATURE_NAME = 's3v4',

AWS_S3_REGION_NAME = 'ap-south-1'

AWS_S3_FILE_OVERWRITE = False

AWS_DEFAULT_ACL = None

AWS_S3_VERITY = True

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


