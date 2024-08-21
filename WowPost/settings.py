from django.core.management.utils import get_random_secret_key
from pathlib import Path
import dj_database_url
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = get_random_secret_key()

DEBUG = False

ALLOWED_HOSTS = ['wow-post.com', 'www.wow-post.com', '216.238.112.24']

# WowPost/settings.py

CSRF_TRUSTED_ORIGINS = [
    'https://wow-post.com',
    'https://www.wow-post.com',
]

AUTH_USER_MODEL = 'Accounts.CustomUser'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Accounts.apps.AccountsConfig',
    'crispy_forms',
    'crispy_bootstrap5',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'WowPost.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'WowPost.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

#CREATE A LOCAL POSTGRESQL DATABASE AND CONNNECT IT BELOW. THIS ALLOWS FOR BETTER QUERY RESPONSE SPEEDS, AVOIDING NETWORK LATENCY.
#SET UP A DATABASE BACKUP

DATABASES = {
    'default': {}
}

DATABASES["default"] = dj_database_url.parse('postgresql://jay:MS7BBuCdQqxlbLt578unQFJX1zoojoOl@dpg-cqm500bqf0us73a5c340-a.ohio-postgres.render.com/wowdbj')

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'standarduse000@gmail.com'
EMAIL_HOST_PASSWORD = 'ogxfuqxgebmxelbt'
DEFAULT_FROM_EMAIL = 'wowpost@localhost'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_REDIRECT_URL = '/home'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


