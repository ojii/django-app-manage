import os
import sys

from django.conf import settings

from .config import DynamicSetting
from .utils import ensure_cleanup
from . import defaults


# Python 3 signature:
#   main(apps, *, argv=sys.argv, environ=os.environ, *args, **kwargs)
def main(apps, *args, **config):
    argv = config.pop('argv', sys.argv)
    environ = config.pop('environ', os.environ)
    full_settings = {}
    # TODO: Once Python 2.6 support can be dropped, switch back to dict comp
    full_settings.update(dict(
        (key, value) for key, value in vars(defaults).items() if key.isupper()
    ))
    argv = list(argv)
    with ensure_cleanup() as cleanup:
        for key, value in config.items():
            if isinstance(value, DynamicSetting):
                cleanup.append(value.cleanup)
                full_settings[key] = value.get_value(argv, environ)
            else:
                full_settings[key] = value

        for arg in args:
            arg.process(argv, environ, full_settings)

        for app in apps:
            if app not in full_settings['INSTALLED_APPS']:
                full_settings['INSTALLED_APPS'].append(app)

        settings.configure(**full_settings)

        from django.core.management import execute_from_command_line

        execute_from_command_line(argv)
