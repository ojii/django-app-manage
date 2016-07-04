#################
django-app-manage
#################

manage.py for your reusable Django applications.


**********
Quickstart
**********

Assuming you have an application named ``my_awesome_app``, add the following to
the root of the project (aka next to ``setup.py``) in a file called
``manage.py``::

    import app_manage

    urlpatterns = []

    if __name__ == '__main__':
        app_manage.main(
            ['my_awesome_app'],
            DATABASES=app_manage.DatabaseConfig(
                env='DATABASE_URL',
                arg='--db-url',
                default='sqlite://localhost/local.sqlite'
            ),
            ROOT_URLCONF='manage',
            STATIC_ROOT=app_manage.TempDir(),
            MEDIA_ROOT=app_manage.TempDir(),
        )


You can now run Django commands such as ``test`` or ``makemssages`` via that
``manage.py`` file.
