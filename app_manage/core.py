import os
import sys

from django.conf import settings

from .config import DEFAULT_SETTINGS
from .config import DynamicSetting
from .utils import ensure_cleanup


def main(apps, argv=sys.argv, environ=os.environ, **configuration):
    full_settings = {}
    full_settings.update(DEFAULT_SETTINGS)
    full_settings['INSTALLED_APPS'] = apps
    argv = list(argv)
    with ensure_cleanup() as cleanup:
        for key, value in configuration.items():
            if isinstance(value, DynamicSetting):
                cleanup.append(value.cleanup)
                full_settings[key] = value.get_value(argv, environ)
            else:
                full_settings[key] = value

        settings.configure(**full_settings)

        from django.core.management import execute_from_command_line

        execute_from_command_line(argv)
