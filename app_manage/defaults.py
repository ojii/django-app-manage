CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

DEBUG = True

DATABASE_SUPPORTS_TRANSACTIONS = True

SITE_ID = 1

USE_I18N = True

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

SECRET_KEY = 'secret-key'

INTERNAL_IPS = ['127.0.0.1']

LANGUAGE_CODE = "en"

LANGUAGES = [
    ('en', 'English')
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher'
]

ALLOWED_HOSTS = ['localhost']

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware'
    'django.middleware.common.CommonMiddleware'
    'django.middleware.csrf.CsrfViewMiddleware'
    'django.contrib.auth.middleware.AuthenticationMiddleware'
    'django.contrib.messages.middleware.MessageMiddleware'
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

INSTALLED_APPS = []
