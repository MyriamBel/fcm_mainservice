import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fcmadminDatabase',
        'USER': 'fcmadminDBAdmin',
        'PASSWORD': 'postgres1',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 60 * 10,  # 10 minutes
    }
}

with open(os.path.join(BASE_DIR, 'fcmadmin/secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

DEBUG = True

ALLOWED_HOSTS = ['localhost', '178.124.179.94', '192.168.1.30']

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

# STATIC_DIR = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [STATIC_DIR]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')