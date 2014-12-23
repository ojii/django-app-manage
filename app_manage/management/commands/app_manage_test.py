from optparse import make_option

from django.core.management import BaseCommand

from .registry import send


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--my-flag',
            action='store',
            dest='my_flag',
            default='flag-no-set'),
        )

    def handle(self, *args, **options):
        send((args, options))
