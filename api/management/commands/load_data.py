import json
import logging

from django.core.management import BaseCommand

from api.models import Joke


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    default_filename = 'data/jokes.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--filename',
            default=self.default_filename,
            help='input filename (.csv)'
        )

        parser.add_argument(
            '-a', '--append',
            dest='replace',
            action='store_false',
            default=True,
            help='Append data (default is to replace).'
        )

    def handle(self, *args, **options):
        if options['replace']:
            logger.info('erasing existing entries')
            Joke.objects.all().delete()

        with open(options['filename']) as f:
            data = json.load(f)

        jokes = []
        for d in data:
            jokes.append(
                Joke(
                    host=d['host'],
                    source=d['source'],
                    date=d['date'],
                    text=d['joke'],
                )
            )

        Joke.objects.bulk_create(jokes)
        print('{} total entries'.format(Joke.objects.count()))
