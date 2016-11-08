from django.core.management.base import BaseCommand, CommandError
from classification_statistics.tasks import calc_accuracy_stat

class Command(BaseCommand):
    help = 'calc_accuracy_stat'

    def handle(self, *args, **options):
        calc_accuracy_stat.delay()
        self.stdout.write('Successfully')