from django.core.management.base import BaseCommand

from courses.core.utils import get_version


class Command(BaseCommand):
    help = 'Show current courses package version'

    def handle(self, *args, **options):
        self.stdout.write(get_version(), ending='')
