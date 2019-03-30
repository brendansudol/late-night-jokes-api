from django.db import models


class ModelBase(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class JokeManager(models.Manager):
    def search(self, params):
        qs = self.get_queryset()

        if params.get('q'):
            qs = qs.filter(text__search=params['q'])

        if params.get('host'):
            qs = qs.filter(host__iexact=params['host'])

        if params.get('year'):
            qs = qs.filter(date__year=params['year'])

        return qs.order_by(params.get('order') or '-date')


class Joke(ModelBase):
    host = models.CharField(max_length=64)
    source = models.CharField(max_length=16)
    date = models.DateField()
    text = models.TextField()

    objects = JokeManager()

    def __str__(self):
        return '{}-{}-{}'.format(self.host, self.date, self.id)

    def to_dict(self):
        fields = ['id', 'host', 'source', 'date', 'text']
        return {f: getattr(self, f) for f in fields}
