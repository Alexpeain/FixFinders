from .base import *
import os
import dj_database_url


SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

RENDER_EXTERNAL_HOSTNAME = [os.environ.get('RENDER_EXTERNAL_HOSTNAME')]
ALLOWED_HOSTS =["fixfinder.onrender.com"]
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files with WhiteNoise
# Insert WhiteNoise after SecurityMiddleware (index 1 is usually correct if Security is 0)
try:
    security_index = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')
    MIDDLEWARE.insert(security_index + 1, 'whitenoise.middleware.WhiteNoiseMiddleware')
except ValueError:
    # Fallback if SecurityMiddleware isn't found
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = os.path.join(BASE_DIR.parent, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
