import abc
import shutil
import tempfile

import dj_database_url

from .utils import NULL

gettext = lambda s: s

DEFAULT_SETTINGS = dict(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    },
    CACHE_MIDDLEWARE_ANONYMOUS_ONLY=True,
    DEBUG=True,
    TEMPLATE_DEBUG=True,
    DATABASE_SUPPORTS_TRANSACTIONS=True,
    SITE_ID=1,
    USE_I18N=True,
    MEDIA_URL='/media/',
    STATIC_URL='/static/',
    ADMIN_MEDIA_PREFIX='/static/admin/',
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    SECRET_KEY='secret-key',
    INTERNAL_IPS=['127.0.0.1'],
    LANGUAGE_CODE="en",
    LANGUAGES=(
        ('en', gettext('English')),
    ),
    PASSWORD_HASHERS=(
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ),
    ALLOWED_HOSTS=['localhost'],
    MIDDLEWARE_CLASSES=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    INSTALLED_APPS=[],
)


class DynamicConfigError(ValueError):
    pass


class DynamicSetting(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_value(self, argv, environ):
        pass

    def cleanup(self):
        pass


class TempDir(DynamicSetting):
    def __init__(self):
        self.tempdir = None

    def get_value(self, argv, environ):
        if self.tempdir is None:
            self.tempdir = tempfile.mkdtemp()
        return self.tempdir

    def cleanup(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)


class Config(DynamicSetting):
    def __init__(self, env=None, arg=None, default=NULL):
        self.env = env
        self.arg = arg
        self.default = default

    def get_value(self, argv, environ):
        value = self.default
        if self.env is not None:
            value = environ.get(self.env, value)
        if self.arg is not None:
            is_flag = isinstance(self.arg, Flag)
            if is_flag:
                arg_name = self.arg.name
            else:
                arg_name = self.arg
            for i, arg in enumerate(list(argv)):
                if arg == arg_name:
                    if is_flag:
                        value = True
                        del argv[i]
                        return value
                    else:
                        try:
                            value = argv[i + 1]
                            del argv[i:i + 2]
                            return value
                        except IndexError:
                            pass
                elif arg.startswith('{}='.format(arg_name)):
                    value = arg[len(arg_name) + 1:]
                    del argv[i]
                    return value
        if value is NULL:
            raise DynamicConfigError("No value found")
        return value


class DatabaseConfig(Config):
    def get_value(self, argv, environ):
        value = super(DatabaseConfig, self).get_value(argv,  environ)
        return {
            'default': dj_database_url.parse(value),
        }


class Flag(object):
    def __init__(self, name):
        self.name = name
