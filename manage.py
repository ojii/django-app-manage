from django.conf.urls import patterns

import app_manage

urlpatterns = patterns('')

if __name__ == '__main__':
    app_manage.main(
        ['test_app'],
        DATABASES=app_manage.DatabaseConfig(
            env='DATABASE_URL',
            arg='--db-url',
            default='sqlite://localhost/local.sqlite'
        ),
        ROOT_URLCONF='manage',
        STATIC_ROOT=app_manage.TempDir(),
        MEDIA_ROOT=app_manage.TempDir(),
    )
