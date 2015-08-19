import abc
import shutil
import tempfile

import dj_database_url

from .utils import NULL
from .utils import with_metaclass

gettext = lambda s: s


class DynamicConfigError(ValueError):
    pass


class DynamicSetting(with_metaclass(abc.ABCMeta)):
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
                elif arg.startswith('{0}='.format(arg_name)):
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


class Argument(object):
    def __init__(self, config, callback):
        self.config = config
        self.callback = callback

    def process(self, argv, environ, settings):
        value = self.config.get_value(argv, environ)
        self.callback(settings, value)
