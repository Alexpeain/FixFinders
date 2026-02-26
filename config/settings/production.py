from .base import *
import os
import dj_database_url

# 1. SECURITY: Debug must be False in production
DEBUG = False

# 2. SECRET KEY: Get from Render Environment Variables
SECRET_KEY = os.environ.get('SECRET_KEY')

# 3. ALLOWED HOSTS: Define who can access your site
ALLOWED_HOSTS = ["fixfinders.onrender.com"]

# Render automatically sets this variable. If it exists, we add it too.
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# CSRF Trusted Origins: Crucial for login to work on Render
CSRF_TRUSTED_ORIGINS = [
    'https://fixfinders.onrender.com',
]

if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

# 4. DATABASE: Configure PostgreSQL connection
# We use the clean syntax that avoids "invalid syntax" errors
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# 5. STATIC FILES: Configure WhiteNoise to serve CSS/Images
# We try to insert it in the correct position (after SecurityMiddleware)
try:
    security_index = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')
    MIDDLEWARE.insert(security_index + 1, 'whitenoise.middleware.WhiteNoiseMiddleware')
except ValueError:
    # Fallback if SecurityMiddleware isn't found
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = os.path.join(BASE_DIR.parent, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 6. SECURITY SETTINGS: Enforce HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 7. LOGGING: Crucial for debugging 500 errors
# This ensures errors are printed to Render logs even when DEBUG=False
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
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
