import os
from pathlib import Path

import cloudinary
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 60 * 10,  # 10 minutes
    }
}
db_from_env = dj_database_url.config(conn_max_age=360)
DATABASES['default'].update(db_from_env)

with open(os.path.join(BASE_DIR, 'fcm-admin/secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

DEBUG = True

ALLOWED_HOSTS = ['*']

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

# STATIC_DIR = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [STATIC_DIR]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')