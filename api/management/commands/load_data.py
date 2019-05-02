import datetime
import json
import logging

from django.core.management import BaseCommand

from api.models import Joke
from api.util import CONAN_KEY, HOST_LOOKUP


logger = logging.getLogger(__name__)


JOKES_ALL_HOSTS_FNAME = 'data/jokes-all-hosts.json'
JOKES_CONAN_FNAME = 'data/jokes-coco.json'


class Command(BaseCommand):
    def add_arguments(self, parser):
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

        jokes = []

        # main jokes file (all hosts - conan)
        with open(JOKES_ALL_HOSTS_FNAME) as f:
            data = json.load(f)

        for d in data:
            if d['host'].lower() == CONAN_KEY:
                continue

            if d['date'] == '2018-09-28':
                continue

            jokes.append(
                Joke(
                    host=HOST_LOOKUP[d['host'].lower()],
                    source='newsmax-{}'.format(d['source']),
                    date=d['date'],
                    text=d['joke'],
                )
            )

        # conan jokes
        with open(JOKES_CONAN_FNAME) as f:
            conan_data = json.load(f)

        for d in conan_data:
            dt = datetime.datetime.strptime(d['credit-date'], '%B %d, %Y')
            # (sometimes, the date from "credit-date" is bad)
            if dt.year < 2000:
                date_str = d['title'].split(' - ')[0]
                try:
                    dt = datetime.datetime.strptime(date_str, '%b %d, %Y')
                except:
                    print('cannot parse date: {}'.format(date_str))
                    continue

            jokes.append(
                Joke(
                    host=HOST_LOOKUP[CONAN_KEY],
                    source='teamcoco-{}'.format(d['id']),
                    date=dt.strftime('%Y-%m-%d'),
                    text=d['body'],
                )
            )

        Joke.objects.bulk_create(jokes)
        print('{} total entries'.format(Joke.objects.count()))
