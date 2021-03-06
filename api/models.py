from random import shuffle

from django.db import models
from django.db.models.functions import Length

from api.util import HOST_LOOKUP


class ModelBase(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class JokeManager(models.Manager):
    def search(self, params):
        qs = self.get_queryset()

        if params.get('query'):
            qs = qs.filter(text__search=params['query'])

        if params.get('year'):
            qs = qs.filter(date__year=params['year'])

        if params.get('host'):
            host = HOST_LOOKUP.get(params['host'].lower())
            if host:
                qs = qs.filter(host__iexact=host)

        if params.get('order') == 'length':
            return qs.order_by(Length('text'))

        return qs.order_by(params.get('order') or '?')

    def rand(self, limit=100):
        # return 3% of entries from table (~1k)
        query = 'SELECT * FROM api_joke TABLESAMPLE BERNOULLI (3);'
        results = [entry.to_dict() for entry in self.raw(query)]

        # one more round of randomizing
        shuffle(results)

        return results[:limit]


class Joke(ModelBase):
    host = models.CharField(max_length=64)
    source = models.CharField(max_length=16)
    date = models.DateField()
    text = models.TextField()

    objects = JokeManager()

    def __str__(self):
        return '{}-{}-{}'.format(self.host, self.date, self.pk)

    def to_dict(self):
        fields = ['id', 'host', 'source', 'date', 'text']
        return {f: getattr(self, f) for f in fields}
