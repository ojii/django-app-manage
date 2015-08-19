###
API
###

.. py:module:: app_manage.core

``app_manage.core``
===================

.. py:function:: main(apps, *, argv=sys.argv, environ=os.environ, *args, **config)

    Main entry point into django-app-manage. Configures Django and then runs
    the command passed in ``argv`` (or ``sys.argv``).

    :param list apps: List of app names (as strings). These will be auto-added to ``INSTALLED_APPS``.
    :param list argv: List of arguments, you shouldn't need to have to set this value yourself.
    :param dict environ: Environment dictionary, you shouldn't need to have to set this value yourself.
    :param args: Arguments to configure your app. Must be instances of :py:class:`app_manage.config.Argument`.
    :param config: Django configuration to use in your app. Values can be instances of :py:class:`app_manage.config.DynamicSetting` subclasses if you want them to be configurable.



.. py:module:: app_manage.config

``app_manage.config``
=====================

.. py:exception:: DynamicConfigError

    Raised by :py:class:`Config` if the argument is used as a flag.


.. py:class:: DynamicSetting

    Base class for all your dynamic settings. Must be subclassed.

    .. py:method:: get_value(argv, environ)

        This method must be implemented by subclasses.

        Given the arguments and environment, returns the value to be used for
        the given setting.

        ``argv`` can and should be modified by this method where applicable.

        :param list argv: List of arguments.
        :param dict environ: Environment dictionary.

    .. py:method:: cleanup

        Optional method that can be used to do any cleanup where necessary
        after the Django command finished executing.


.. py:class:: TempDir

    :py:class:`DynamicSetting` subclass that returns a path to a temporary
    directory and removes that directory after the Django command executed.

    Useful for ``MEDIA_ROOT`` and similar settings.


.. py:class:: Config(env=None, arg=None, default=NULL)

    The bread-and-butter class to configure your app. ``env`` is the key in the
    environment dictionary and ``arg`` the name of the command line argument
    (must include leading dashes, for example ``'--arg'``).

    Command line arguments override environment variables.


.. py:class:: DatabaseConfig

    Helper class that runs the value passed through dj_database_url.


.. py:class:: Flag(name)

    Can be used as the ``arg`` argument to a :py:class:`Config` instance to
    indicate a boolean flag instead of a command line argument.


.. py:class:: Argument(config, callback)

    Class used to do more complex configurations that affect multiple settings.
    Instances of this class are passed as ``args`` to :py:func:`app_manage.core.main`.

    ``config`` is an instance of a :py:class:`DynamicSetting` subclass and
    ``callback`` is a callable with the following signature:

    .. py:function:: callback(settings, value)

        :param dict settings: Dictionary holding Django settings
        :param value: The value returned by ``config``.
