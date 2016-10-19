from django.core.management.base import BaseCommand, CommandError
from classification_statistics.tasks import calculate_classification_statistics

class Command(BaseCommand):
    help = 'calculate_classification_statistics'

    def handle(self, *args, **options):
        calculate_classification_statistics.delay()
        self.stdout.write('Successfully')